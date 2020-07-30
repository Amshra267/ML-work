os.makedirs('models')  # create directory for model save
os.makedirs('models_weights') # create directory for model weights save
import gc

meta_train = []
meta_labs = []
meta_test = []

def model_perform(labels,model,preprocessfn,learning_rate = 0.001):


    # performing kfold cross validation along with data generators
    VALIDATION_ACCURACY = []
    VALIDAITON_LOSS = []

    no = 1
    

    for train,val in skf.split(np.zeros(len(labels)),labels[['label']]):

        # split train and val data
        train_data = labels.iloc[train]
        val_data = labels.iloc[val]


        # performing data augmentation
        train_generator = data_augmentation(preprocessfn, batch_size, size, 'train', train_path,train_data)
        val_generator = data_augmentation(preprocessfn, batch_size, size,'valid',train_path, val_data)


        # plot some images
        plotImages(train_generator)

        # create model
        model1 = model

        # compiling this model
        model1.compile(loss='sparse_categorical_crossentropy', 
              optimizer=optimizers.Adam(),
              metrics=['accuracy'])

    # getting callbacks
        callbacks_list = callbacks(file_path = "models_weights/model_"+str(no)+".h5")
        
        # fit model
        history = model1.fit(train_generator,
                                  steps_per_epoch= (len(train_data)//batch_size),
                                  epochs = epochs, 
                                  validation_data = val_generator,
                                  validation_steps = (len(val_data)//batch_size),
                                  shuffle=True, 
                                  verbose=True,
                                  callbacks=callbacks_list)

        model1.save('models/model' + str(no))

        #PLOT HISTORY:

        model_visualisation_graph(history)
        
        # defining test_gen
        test_gen = data_augmentation(preprocessfn, batch_size, size, 'test',test_path,train_data)
        

        # LOAD BEST MODEL to evaluate the performance of the model
        model1.load_weights("models_weights/model_"+str(no)+".h5")

        results = model1.evaluate(val_generator)
        val_stat = predict(val_generator,model1)
        test_stat = predict(test_gen,model1)
        meta_test.append(test_stat)
            
        # for plotting confusion_matrix of train_data
        label_index = {v: k for k,v in val_generator.class_indices.items()}
        check_labs = [label_index[int(p)] for p in val_stat[0][:]]
        print(check_labs)
        print(len(check_labs))
        meta_train.append(val_stat[1])

        # now considering actual labels of train_data
        actual_labs = [label_index[int(p)] for p in val_generator.classes]
        print(actual_labs)
        print(len(actual_labs))
        meta_labs.append(actual_labs)
        
        # reports for train data
        report,confusion = classify_report(actual_labs,check_labs)

        # plotting confusion matrix
        plot_confusion_matrix(confusion, classes=['0','1'],
                                  normalize=False,
                                  title='Confusion matrix',
                                  cmap=plt.cm.Blues)

        print(report)
        
        results = dict(zip(model.metrics_names,results))

        VALIDATION_ACCURACY.append(results['accuracy'])
        VALIDATION_LOSS.append(results['loss'])
        
        
        K.clear_session()

        no += 1
    
    del train_generator
    gc.collect()
    return val_stat, VALIDATION_ACCURACY , VALIDAITON_LOSS, test_stat,val_gen
    
